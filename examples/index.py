"""Generate code examples for docs home page."""
import maxgradient as mg
styles = {
    "import": "#FC77C4",
    "keyword": "#FC77C4",
    "class": "#8BE9FD",
    "func": "#50FA7B",
    "str": "#F1FA8C",
    "int": "#BD93F9",
    "text": "#dddddd"
    
}
console = mg.Console(width=70, record=True, theme=styles)


console.print(
    "[keyword]import[/][text] maxgradient[/][keyword] as[/][text] mg[/]")
console.line()
console.print(
console.gradient("Hello, World!")