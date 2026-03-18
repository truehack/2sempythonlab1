import pytest
import json
from main import Task, TaskSource, TaskGenerator, FileSource, ApiSource, process_tasks


def test_task():
    task = Task(id=1, payload="test payload")
    assert task.id == 1
    assert task.payload == "test payload"


def test_generator_count():
    gen = TaskGenerator(3)
    tasks = list(gen.get_tasks())
    assert len(tasks) == 3
    assert tasks[0].id == 0
    assert tasks[0].payload == "Задача номер 0"


def test_generator_zero():
    gen = TaskGenerator(0)
    assert len(list(gen.get_tasks())) == 0


def test_generator_contract():
    source = TaskGenerator(5)
    assert isinstance(source, TaskSource)


def test_file_source_with_file(tmp_path):
    file_path = tmp_path / "test_tasks.json"
    data = [{"id": 100, "payload": "Из файла заказ"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")
    
    source = FileSource(str(file_path))
    tasks = list(source.get_tasks())
    assert len(tasks) == 1
    assert tasks[0].id == 100


def test_file_source_not_found():
    source = FileSource("non_existent_file.json")
    tasks = list(source.get_tasks())
    assert len(tasks) == 0


def test_file_contract(tmp_path):
    file_path = tmp_path / "test.json"
    file_path.write_text("[]", encoding="utf-8")
    source = FileSource(str(file_path))
    assert isinstance(source, TaskSource)


def test_api_source():
    data = [{"id": 500, "payload": "API данные"}]
    source = ApiSource(raw_data=data)
    task = next(source.get_tasks())
    assert task.id == 500


def test_api_empty():
    source = ApiSource()
    assert len(list(source.get_tasks())) == 0


def test_api_contract():
    source = ApiSource(raw_data=[])
    assert isinstance(source, TaskSource)


def test_process_works():
    gen = TaskGenerator(2)
    process_tasks(gen)


def test_process_bad():
    class WrongSource:
        pass
    with pytest.raises(TypeError):
        process_tasks(WrongSource())
        
def test_file_source_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("not valid json", encoding="utf-8")
    source = FileSource(str(file_path))
    assert len(list(source.get_tasks())) == 0
