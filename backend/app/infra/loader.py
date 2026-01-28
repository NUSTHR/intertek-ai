from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any

import yaml

from ..domain.models import Engine, ModuleDef, QuestionDef, RouterRuleDef, VariableDef, VariableRuleDef


class EngineLoader:
    def __init__(self, data_dir: Path, cache_ttl_seconds: int = 0) -> None:
        self.data_dir = data_dir
        self._cache: tuple[tuple[tuple[str, float], ...], Engine] | None = None
        self._cache_ttl_seconds = cache_ttl_seconds
        self._last_checked = 0.0

    def get_engine(self) -> Engine:
        now = time.time()
        if self._cache and self._cache_ttl_seconds > 0 and (now - self._last_checked) < self._cache_ttl_seconds:
            return self._cache[1]
        signature = tuple(sorted((p.name, p.stat().st_mtime) for p in self.data_dir.glob("*.yaml")))
        self._last_checked = now
        if self._cache and self._cache[0] == signature:
            return self._cache[1]
        engine = self._load_engine()
        self._cache = (signature, engine)
        return engine

    def _load_engine(self) -> Engine:
        if not self.data_dir.exists():
            raise RuntimeError("resources_dir_missing")
        files = sorted(self.data_dir.glob("*.yaml"))
        constants: dict[str, Any] = {}
        const_path = self.data_dir / "constants.yaml"
        if const_path.exists():
            const_raw = yaml.safe_load(const_path.read_text(encoding="utf-8")) or {}
            constants = const_raw.get("constants") if isinstance(const_raw, dict) else {}
        modules: list[ModuleDef] = []
        questions_by_id: dict[str, QuestionDef] = {}
        for path in files:
            raw_text = path.read_text(encoding="utf-8")
            raw_text = raw_text.replace("[cite_end]", "")
            raw_text = re.sub(r"\[cite:[^\]]*\]", "", raw_text)
            raw = yaml.safe_load(raw_text) or {}
            module_id_raw = raw.get("module_id") or raw.get("module")
            if module_id_raw is None:
                raise RuntimeError(f"module_id_missing:{path.name}")
            module_id = str(module_id_raw)
            module_num = self._parse_module_number(module_id_raw, path.name)
            questions_raw = raw.get("questions") or []
            questions: list[QuestionDef] = []
            for q in questions_raw:
                qid = q.get("id")
                if not qid:
                    continue
                questions.append(
                    QuestionDef(
                        id=str(qid),
                        qtype=q.get("type") or "",
                        dependency=q.get("dependency"),
                        options=q.get("options"),
                        raw=q,
                    )
                )
            questions_by_id_local = {q.id: q for q in questions}
            variables_raw = raw.get("variables") or []
            variables: list[VariableDef] = []
            for var in variables_raw:
                name = var.get("name")
                if not name:
                    continue
                rules_raw = var.get("rules") or []
                rules = [
                    VariableRuleDef(condition=str(rule.get("condition") or ""), value=rule.get("value"))
                    for rule in rules_raw
                ]
                variables.append(
                    VariableDef(
                        name=str(name),
                        var_type=var.get("type"),
                        initial_value=var.get("initial_value"),
                        rules=rules,
                    )
                )
            router_raw = raw.get("router") or []
            router: list[RouterRuleDef] = []
            for rule in router_raw:
                target_module_id = None
                if "target_module_id" in rule:
                    target_module_id = str(rule.get("target_module_id"))
                elif "target_module" in rule:
                    target_module_id = self._parse_target_module(rule.get("target_module"))
                router.append(
                    RouterRuleDef(
                        condition=str(rule.get("condition") or ""),
                        action=str(rule.get("action") or ""),
                        target_module_id=target_module_id,
                        message=rule.get("message"),
                    )
                )
            modules.append(
                ModuleDef(
                    module_id=module_id,
                    module_num=module_num,
                    title=raw.get("title") or module_id,
                    description=raw.get("description"),
                    questions=questions,
                    questions_by_id=questions_by_id_local,
                    variables=variables,
                    router=router,
                )
            )
            questions_by_id.update(questions_by_id_local)
        modules.sort(key=lambda m: m.module_num)
        modules_by_id = {m.module_id: m for m in modules}
        return Engine(modules=modules, modules_by_id=modules_by_id, questions_by_id=questions_by_id, constants=constants)

    @staticmethod
    def _parse_module_number(module_id: Any, filename: str) -> int:
        if isinstance(module_id, int):
            return module_id
        if isinstance(module_id, str):
            match = re.search(r"\d+", module_id)
            if match:
                return int(match.group(0))
        match = re.search(r"\d+", filename)
        if match:
            return int(match.group(0))
        return 9999

    @staticmethod
    def _parse_target_module(raw: Any) -> str | None:
        if raw is None:
            return None
        if isinstance(raw, int):
            return str(raw)
        if isinstance(raw, str):
            match = re.search(r"\d+", raw)
            if match:
                return match.group(0)
        return None
