{
    "name": "proyecto_dam",
    "summary": """
        TODO Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        TODO This app helps you to manage a business of printing customized t-shirts
        for online customers. It offers a public page allowing customers to make
        t-shirt orders.

        Note that this is just a toy app intended to learn the javascript
        framework.
    """,
    "author": "Carlos Griñán",
    "category": "Productivity",
    "version": "0.1",
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "data/sources.xml",
        "views/views.xml",
    ],
    # "demo": [
    #     "demo/demo.xml",
    # ],
    "assets": {
        "web.assets_backend": [
            "proyecto_dam/static/src/**/*",
            "proyecto_dam/static/img/**/*",
        ],
        # "web.assets_common": [
        #     "web/static/lib/bootstrap/**/*",
        # ],
    },
    "depends": [
        "base",
        "web",
    ],
}
