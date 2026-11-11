"""Unit tests for agent-migration-idempotency-checker."""
import unittest
from agent_migration_idempotency_checker.checker import MigrationIdempotencyChecker

class TestMigrationIdempotencyChecker(unittest.TestCase):
    def setUp(self):
        self.checker = MigrationIdempotencyChecker()

    def test_clean_idempotent_script(self):
        up = "CREATE TABLE IF NOT EXISTS orders (id INT); CREATE INDEX IF NOT EXISTS idx_o_id ON orders(id);"
        down = "DROP TABLE IF EXISTS orders;"
        v = self.checker.check_migration(up, down)
        self.assertTrue(v.is_idempotent)
        self.assertTrue(v.has_rollback_support)

    def test_missing_guard_detected(self):
        up = "CREATE TABLE customers (id INT);"
        v = self.checker.check_migration(up)
        self.assertFalse(v.is_idempotent)
        self.assertIn("customers", v.missing_guards[0])
