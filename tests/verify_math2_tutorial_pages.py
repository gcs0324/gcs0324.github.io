from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "kaoyan-math2-110.html",
    "kaoyan-math2-limit.html",
    "kaoyan-math2-derivative.html",
    "kaoyan-math2-integral.html",
    "kaoyan-math2-multivariable.html",
    "kaoyan-math2-ode.html",
    "kaoyan-math2-matrix.html",
    "kaoyan-math2-vector-equations.html",
    "kaoyan-math2-eigen-quadratic.html",
]
TOPICS = PAGES[1:]
HEADERS = ["知识点", "优先级", "要不要学", "考频", "经验分值", "考察题型", "学到什么程度"]
PROCEDURES = {
    "kaoyan-math2-limit.html": 2,
    "kaoyan-math2-derivative.html": 3,
    "kaoyan-math2-integral.html": 3,
    "kaoyan-math2-multivariable.html": 1,
    "kaoyan-math2-ode.html": 1,
    "kaoyan-math2-matrix.html": 0,
    "kaoyan-math2-vector-equations.html": 1,
    "kaoyan-math2-eigen-quadratic.html": 1,
}
DETAILED_PROCEDURES = {
    "kaoyan-math2-limit.html": 1,
    "kaoyan-math2-derivative.html": 1,
}


class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.nav_depth = 0
        self.nav_hrefs = []
        self.local_pages = []
        self.matrix_depth = 0
        self.in_th = False
        self.th = ""
        self.headers = []
        self.priority = set()
        self.frequency = set()
        self.examples = 0
        self.theme_css = False
        self.theme_js = False
        self.procedures = 0
        self.procedure_steps = []
        self._procedure_depth = 0
        self._current_steps = 0
        self.procedure_signals = 0
        self.procedure_checks = 0
        self.procedure_mistakes = 0
        self.detailed_procedures = 0
        self.procedure_visuals = 0
        self.procedure_examples = 0
        self.procedure_memories = 0
        self.procedure_detail_steps = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "nav":
            self.nav_depth += 1
        if tag == "a" and attrs.get("href"):
            href = attrs["href"]
            if self.nav_depth and href.startswith("#"):
                self.nav_hrefs.append(href)
            if href.endswith(".html"):
                self.local_pages.append(href)
        if tag == "table" and "matrix" in classes:
            self.matrix_depth += 1
        if tag == "th" and self.matrix_depth:
            self.in_th = True
            self.th = ""
        if tag == "span" and self.matrix_depth:
            if "pri" in classes:
                self.priority.update(set(classes) & {"a", "b", "c"})
            if "freq" in classes:
                self.frequency.update(set(classes) & {"vh", "hi", "mid", "low"})
        if "ex" in classes:
            self.examples += 1
        if "procedure" in classes:
            self.procedures += 1
            self._procedure_depth += 1
            self._current_steps = 0
        if self._procedure_depth and "procedure-step" in classes:
            self._current_steps += 1
        if self._procedure_depth and "procedure-signal" in classes:
            self.procedure_signals += 1
        if self._procedure_depth and "procedure-check" in classes:
            self.procedure_checks += 1
        if self._procedure_depth and "procedure-mistake" in classes:
            self.procedure_mistakes += 1
        if "procedure-detailed" in classes:
            self.detailed_procedures += 1
        if "procedure-visual" in classes:
            self.procedure_visuals += 1
        if "procedure-example" in classes:
            self.procedure_examples += 1
        if "procedure-memory" in classes:
            self.procedure_memories += 1
        if "procedure-detail-step" in classes:
            self.procedure_detail_steps += 1
        if tag == "link" and attrs.get("href") == "../shared/theme.css":
            self.theme_css = True
        if tag == "script" and attrs.get("src") == "../shared/theme.js":
            self.theme_js = True

    def handle_endtag(self, tag):
        if tag == "nav":
            self.nav_depth -= 1
        if tag == "th" and self.in_th:
            self.headers.append(" ".join(self.th.split()))
            self.in_th = False
        if tag == "table" and self.matrix_depth:
            self.matrix_depth -= 1
        if tag == "article" and self._procedure_depth:
            self.procedure_steps.append(self._current_steps)
            self._procedure_depth -= 1

    def handle_data(self, data):
        if self.in_th:
            self.th += data


def main():
    missing = [name for name in PAGES if not (ROOT / "doc" / name).exists()]
    assert not missing, f"missing math pages: {missing}"

    for name in TOPICS:
        path = ROOT / "doc" / name
        audit = Audit()
        audit.feed(path.read_text())
        assert audit.theme_css and audit.theme_js, f"{name}: shared theme missing"
        assert audit.headers[:7] == HEADERS, f"{name}: decision headers {audit.headers[:7]}"
        assert audit.priority == {"a", "b", "c"}, f"{name}: priority labels {audit.priority}"
        assert audit.frequency == {"vh", "hi", "mid", "low"}, f"{name}: frequency labels {audit.frequency}"
        assert audit.examples >= 3, f"{name}: only {audit.examples} tutorial examples"
        expected_procedures = PROCEDURES[name]
        assert audit.procedures == expected_procedures, f"{name}: procedure cards {audit.procedures}, expected {expected_procedures}"
        if expected_procedures:
            assert "procedures" in audit.ids, f"{name}: procedures anchor missing"
            assert audit.procedure_signals == expected_procedures, f"{name}: procedure signals missing"
            assert audit.procedure_checks == expected_procedures, f"{name}: procedure checks missing"
            assert audit.procedure_mistakes == expected_procedures, f"{name}: procedure mistakes missing"
            assert all(steps >= 4 for steps in audit.procedure_steps), f"{name}: procedure steps {audit.procedure_steps}"
        expected_detailed = DETAILED_PROCEDURES.get(name, 0)
        assert audit.detailed_procedures == expected_detailed, f"{name}: detailed procedures {audit.detailed_procedures}, expected {expected_detailed}"
        if expected_detailed:
            assert audit.procedure_visuals >= expected_detailed, f"{name}: detailed procedure visual missing"
            assert audit.procedure_examples >= expected_detailed, f"{name}: detailed procedure example missing"
            assert audit.procedure_memories >= expected_detailed, f"{name}: detailed procedure memory missing"
            assert audit.procedure_detail_steps >= 4 * expected_detailed, f"{name}: detailed steps {audit.procedure_detail_steps}"
        assert not [href for href in audit.nav_hrefs if href[1:] not in audit.ids], f"{name}: broken nav anchor"
        for href in audit.local_pages:
            assert (path.parent / href).exists(), f"{name}: missing linked page {href}"

    index = (ROOT / "index.html").read_text()
    for name in PAGES:
        assert index.count("doc/" + name) == 2, f"index entry count for {name}"
    print("Math II tutorial QA PASS: 9 pages, matrices, labels, examples, anchors, links and index")


if __name__ == "__main__":
    main()
