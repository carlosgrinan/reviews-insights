{
    "name": "reviews_insights",
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
    "assets": {
        "web.assets_backend": [
            "reviews_insights/static/src/**/*",
            "reviews_insights/static/img/*",
        ],
    },
    "depends": ["base", "web", "bus", "queue_job"],
    "external_dependencies": {
        "python": ["requests", "google-api-python-client", "google-auth", "googlemaps", "openai", "python-dotenv"]
    },
}
