from jaypore_ci.interfaces import Reporter, Status


class Text(Reporter):
    def render(self, pipeline):
        """
        Returns a human readable report for a given pipeline.
        """
        return f"""
<details>
    <summary>JayporeCi: {pipeline.get_status_dot()} {pipeline.remote.sha[:10]}</summary>

{self.__render_graph__(pipeline)}

</details>"""

    def __render_graph__(self, pipeline) -> str:  # pylint: disable=too-many-locals
        """
        Render a plaintext graph given the jobs in the pipeline.
        """
        st_map = {
            Status.RUNNING: "🔵",
            Status.FAILED: "🔴",
            Status.PASSED: "🟢",
        }
        graph = ["```"]
        for stage in pipeline.stages:
            nodes, edges = set(), set()
            for job in pipeline.jobs.values():
                if job.stage != stage:
                    continue
                nodes.add(job.name)
                edges |= {(p, job.name) for p in job.parents}
            if not nodes:
                continue
            graph += [f"┏━ {stage}", "┃"]
            max_name = max(len(job) for job in nodes)
            for n in sorted(
                nodes, key=lambda x: len(pipeline.jobs[x].parents)
            ):  # Fewer parents first
                n = pipeline.jobs[n]
                name = (n.name + " " * max_name)[:max_name]
                status = st_map.get(n.status, "🟡")
                run_id = f"{n.run_id}"[:8] if n.run_id is not None else ""
                if n.parents:
                    graph += [f"┃ {status} : {name} [{run_id:<8}] ← {n.parents}"]
                else:
                    graph += [f"┃ {status} : {name} [{run_id:<8}]"]
            graph += ["┗━━━━━━━━━━━━━━━"]
        graph += ["```"]
        return "\n".join(graph)
