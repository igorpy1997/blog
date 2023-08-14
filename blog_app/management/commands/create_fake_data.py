# blog_app/management/commands/create_fake_data.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
from blog_app.factories import CustomUserFactory, PostFactory, CommentFactory, LikeFactory


class Command(BaseCommand):
    help = "Creates fake data for testing purposes"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of instances to create")

    def handle(self, *args, **options):
        count = options["count"]

        # Create a user (this will be used as an author for all posts, comments, and likes)
        user = CustomUserFactory()

        # Create fake data using factories
        for _ in range(count):
            post = PostFactory(author=user)
            comment = CommentFactory(post=post, author=user)
            like = LikeFactory(author=user, post=post)

        # Use Django"s dumpdata command to create a human-readable fixture
        call_command("dumpdata", "blog_app", indent=2, output="initial_data.json")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} instances and generated the human-readable fixture")
        )
