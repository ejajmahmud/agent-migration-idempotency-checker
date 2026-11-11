"""CLI for agent-migration-idempotency-checker."""
import sys
import argparse
from .checker import MigrationIdempotencyChecker

def main():
    parser = argparse.ArgumentParser(description="Agent Migration Idempotency Checker CLI")
    parser.add_argument("--demo", action="store_true", help="Check sample migration script")
    args = parser.parse_args()

    if args.demo:
        checker = MigrationIdempotencyChecker()
        bad_up = "CREATE TABLE users (id SERIAL PRIMARY KEY); CREATE INDEX idx_users_id ON users (id);"
        verdict = checker.check_migration(bad_up, down_sql="DROP TABLE IF EXISTS users;")
        print(f"Idempotent: {verdict.is_idempotent}")
        print(f"Missing Guards: {verdict.missing_guards}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
