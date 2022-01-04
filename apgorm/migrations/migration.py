# MIT License
#
# Copyright (c) 2021 TrigonDev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import json
from pathlib import Path

from .describe import Describe


class Migration:
    def __init__(self, describe: Describe, migrations: str, path: Path):
        self.describe = describe
        self.migrations = migrations
        self.path = path

    @property
    def migration_id(self) -> int:
        return self.id_from_path(self.path)

    @classmethod
    def load_all_migrations(cls, folder: Path) -> list[Migration]:
        migrations: list[Migration] = []
        for p in folder.glob("*"):
            if p.is_file():
                continue

            try:
                migrations.append(cls.from_path(p))
            except FileNotFoundError:
                continue

        return migrations

    @classmethod
    def load_last_migration(cls, folder: Path) -> Migration | None:
        migrations = cls.load_all_migrations(folder)
        if len(migrations) == 0:
            return None
        migrations.sort(key=lambda m: m.migration_id)
        return migrations[-1]

    @classmethod
    def create_migration(
        cls, describe: Describe, migrations: str, folder: Path
    ) -> Migration:
        last_migration = cls.load_last_migration(folder)
        if last_migration:
            next_id = last_migration.migration_id + 1
        else:
            next_id = 0
        next_path = folder / str(next_id)
        next_path.mkdir(parents=True, exist_ok=False)
        with (next_path / "describe.json").open("w+") as f:
            f.write(json.dumps(describe.todict(), indent=4))
        with (next_path / "migrations.sql").open("w+") as f:
            f.write(migrations)

        return cls(describe, migrations, next_path)

    @classmethod
    def from_path(cls, path: Path) -> Migration:
        with (path / "describe.json").open("r") as f:
            describe = Describe(**json.loads(f.read()))

        with (path / "migrations.sql").open("r") as f:
            sql = f.read()

        return cls(describe, sql, path)

    @staticmethod
    def path_from_id(migration_id: int, folder: Path) -> Path:
        return folder / str(migration_id)

    @staticmethod
    def id_from_path(path: Path) -> int:
        return int(path.name)
