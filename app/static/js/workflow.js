document.addEventListener("DOMContentLoaded", () => {

    function clearHighlights() {

        document.querySelectorAll(".timeline-event")
            .forEach(el => {
                el.classList.remove("active-event");
            });

        document.querySelectorAll(".mermaid svg g.node rect")
            .forEach(node => {
                node.style.stroke = "";
                node.style.strokeWidth = "";
            });

    }

    // =========================
    // TIMELINE -> WORKFLOW
    // =========================

    document.body.addEventListener("click", (event) => {

        const timelineItem = event.target.closest(".timeline-event");

        if (!timelineItem) {
            return;
        }

        clearHighlights();

        timelineItem.classList.add("active-event");

        const eventId = timelineItem.dataset.eventId;

        const mermaidNodes =
            document.querySelectorAll(`[id*="E${eventId}"] rect`);

        mermaidNodes.forEach(node => {

            node.style.strokeWidth = "4px";
            node.style.stroke = "#dc3545";

        });

    });

    // =========================
    // WORKFLOW -> TIMELINE
    // =========================

    document.body.addEventListener("click", (event) => {

        const node = event.target.closest("g.node");

        if (!node) {
            return;
        }

        clearHighlights();

        const nodeId = node.id;

        const match = nodeId.match(/E(\d+)/);

        if (!match) {
            return;
        }

        const eventId = match[1];

        const timelineItem = document.querySelector(
            `.timeline-event[data-event-id="${eventId}"]`
        );

        if (!timelineItem) {
            return;
        }

        timelineItem.classList.add("active-event");

        const rect = node.querySelector("rect");

        if (rect) {

            rect.style.strokeWidth = "4px";
            rect.style.stroke = "#dc3545";

        }

        timelineItem.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    });

});