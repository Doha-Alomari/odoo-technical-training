import base64
import os


def set_company_branding(env):
    company = env["res.company"].search([], limit=1)

    if not company:
        return

    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "static",
        "src",
        "img",
        "Rami's Bike Workshop.png",
    )

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as logo_file:
            logo = base64.b64encode(logo_file.read())

        company.write({
            "name": "Rami's Bike Workshop",
            "logo": logo,
        })


def post_init_hook(env):
    set_company_branding(env)