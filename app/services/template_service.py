from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

def render_template(nombre_template, expediente):
    template = env.get_template(nombre_template)

    actor = next((p for p in expediente.partes if p.tipo == "actor"), None)
    demandado = next((p for p in expediente.partes if p.tipo == "demandado"), None)

    return template.render(
        expediente=expediente,
        actor=actor,
        demandado=demandado
    )