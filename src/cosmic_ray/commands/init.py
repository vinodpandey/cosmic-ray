"Implementation of the 'init' command."
import logging
from typing import Iterable
import uuid

from cosmic_ray.ast import get_ast, ast_nodes
import cosmic_ray.modules
from cosmic_ray.config import ConfigDict
from cosmic_ray.work_item import MutationSpec, ResolvedMutationSpec, WorkItem
from cosmic_ray.plugins import get_operator
from cosmic_ray.work_db import WorkDB

log = logging.getLogger()


def _all_work_items(module_paths, operator_names, config: ConfigDict = None) -> Iterable[WorkItem]:
    "Iterable of all WorkItems for the given inputs."
    start_limit = config.get("start-limit", 0) if config else 0
    end_limit = config.get("end-limit", 0) if config else 0

    for module_path in module_paths:
        module_ast = get_ast(module_path)

        for op_name in operator_names:
            operator = get_operator(op_name)()

            positions = (
                (start_pos, end_pos)
                for node in ast_nodes(module_ast)
                for start_pos, end_pos in operator.mutation_positions(node)
            )

            for occurrence, (start_pos, end_pos) in enumerate(positions):
                if start_limit and end_limit:
                    if start_pos[0] >= start_limit and end_pos[0] <= end_limit:
                        mutation = ResolvedMutationSpec(
                            module_path=str(module_path),
                            operator_name=op_name,
                            occurrence=occurrence,
                            start_pos=start_pos,
                            end_pos=end_pos,
                        )

                        yield WorkItem.single(job_id=uuid.uuid4().hex, mutation=mutation)
                else:
                    mutation = ResolvedMutationSpec(
                        module_path=str(module_path),
                        operator_name=op_name,
                        occurrence=occurrence,
                        start_pos=start_pos,
                        end_pos=end_pos,
                    )

                    yield WorkItem.single(job_id=uuid.uuid4().hex, mutation=mutation)


def init(module_paths, work_db: WorkDB, config: ConfigDict = None):
    """Clear and initialize a work-db with work items.

    Any existing data in the work-db will be cleared and replaced with entirely
    new work orders. In particular, this means that any results in the db are
    removed.

    Args:
      module_paths: iterable of pathlib.Paths of modules to mutate.
      work_db: A `WorkDB` instance into which the work orders will be saved.
    """

    operator_names = list(cosmic_ray.plugins.operator_names())

    work_db.clear()
    work_db.add_work_items(_all_work_items(module_paths, operator_names, config))
