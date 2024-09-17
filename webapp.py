import os
from app import create_app, db
from app.models import (
    AmazonAnalysis,
    FacebookAnalysis,
    InstagramAnalysis,
    JumiaAnalysis,
    KongaAnalysis,
    TwitterAnalysis,
    User,
    StripeCustomer,
    Task,
)
from flask_migrate import Migrate, upgrade

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_Shell_context():
    return dict(
        db=db,
        User=User,
        StripeCustomer=StripeCustomer,
        FacebookAnalysis=FacebookAnalysis,
        InstagramAnalysis=InstagramAnalysis,
        TwitterAnalysis=TwitterAnalysis,
        KongaAnalysis=KongaAnalysis,
        AmazonAnalysis=AmazonAnalysis,
        JumiaAnalysis=JumiaAnalysis,
        Task=Task,
    )


@app.cli.command()
def test():
    """Run the unit tests."""

    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def deploy():
    """Run deployementt tasks"""

    # migrate database to the latest revision
    upgrade()
