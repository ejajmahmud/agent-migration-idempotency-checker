"""Core Migration Idempotency Checker implementation."""
import re
from dataclasses import dataclass
from typing import List

@dataclass
class MigrationVerdict:
    is_idempotent: bool
    has_rollback_support: bool
    missing_guards: List[str]
    issues: List[str]

class MigrationIdempotencyChecker:
    """Verifies that database schema migrations can run multiple times and rollback cleanly."""
    
    def check_migration(self, up_sql: str, down_sql: Optional[str] = None) -> MigrationVerdict:
        issues = []
        missing_guards = []

        # 1. Check for CREATE TABLE without IF NOT EXISTS
        create_tables = re.findall(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)", up_sql, re.IGNORECASE)
        for tbl in create_tables:
            if tbl.upper() != "IF" and not re.search(rf"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+{tbl}", up_sql, re.IGNORECASE):
                missing_guards.append(f"CREATE TABLE '{tbl}' lacks 'IF NOT EXISTS'")

        # 2. Check for CREATE INDEX without IF NOT EXISTS
        create_indexes = re.findall(r"CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)", up_sql, re.IGNORECASE)
        for idx in create_indexes:
            if idx.upper() != "IF" and not re.search(rf"CREATE\s+(?:UNIQUE\s+)?INDEX\s+IF\s+NOT\s+EXISTS\s+{idx}", up_sql, re.IGNORECASE):
                missing_guards.append(f"CREATE INDEX '{idx}' lacks 'IF NOT EXISTS'")

        # 3. Check for rollback script
        has_rollback = bool(down_sql and down_sql.strip())
        if not has_rollback:
            issues.append("Missing corresponding down migration script.")

        is_idempotent = len(missing_guards) == 0

        return MigrationVerdict(
            is_idempotent=is_idempotent,
            has_rollback_support=has_rollback,
            missing_guards=missing_guards,
            issues=issues
        )
