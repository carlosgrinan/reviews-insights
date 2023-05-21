{
    "name": "proyecto_dam",
    "summary": """
        AI-powered brief insights on customer feedback.""",
    "description": """
        This app provide  insights on customer feedback from various text-based sources, such as customer support emails and reviews, which are processed by OpenAI's GPT-3.5.
    """,
    "author": "Carlos Grinan",
    "category": "Productivity",
    "version": "0.1",
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "data/sources.xml",
        "views/views.xml",
    ],
    # TODO like "data/sources.xml", but with summaries and refres tokens for each source
    # "demo": [
    #     "demo/sources.xml",
    # ],
    "assets": {
        "web.assets_backend": [
            "proyecto_dam/static/src/**/*",
            "proyecto_dam/static/img/**/*",
        ],
    },
    "depends": [
        "base",
        "web",
    ],
}
