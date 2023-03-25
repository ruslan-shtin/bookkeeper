from bookkeeper.repository.sqlite_repository import SQliteRepository
from bookkeeper.models.category import Category

import pytest

repo = SQliteRepository('test_sq.db', Category)


def obj_ass(left: Category, right: Category):
    assert str(left.name) == str(right.name)
    assert str(left.parent) == str(right.parent)
    assert str(left.pk) == str(right.pk)


def test_crud():
    # test_add
    obj = Category('John', 4)
    pk = repo.add(obj)
    assert obj.name == 'John'

    # test_get
    obj_get: Category = repo.get(pk)
    obj_ass(obj, obj_get)

    # test_update
    obj2 = Category('alice', 4)
    obj2.pk = pk
    repo.update(obj2)
    obj_get: Category = repo.get(pk)
    obj_test: Category = Category('alice', 4)
    obj_test.pk = pk
    obj_ass(obj_get, obj_test)

    # test_delete
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk():
    pass
    obj: Category = Category('al', 5)
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk():
    with pytest.raises(AttributeError):
        repo.add(0)


def test_cannot_delete_not_exist():
    with pytest.raises(KeyError):
        repo.delete(10)


def test_cannot_update_without_pk():
    obj: Category = Category('al', 1)
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all():
    objects: list[Category] = [Category(f'al{i}', i*i) for i in range(5)]
    for o in objects:
        repo.add(o)

    all = repo.get_all()
    for o, o_all in zip(objects, all):
        obj_ass(o, o_all)
    for o in objects:
        repo.delete(o.pk)


def test_get_all_with_condition():
    objects = []
    for i in range(5):
        o = Category('', 2)
        o.name = str(i)
        o.parent = 897
        repo.add(o)
        objects.append(o)
    obj_pk = [obj.pk for obj in repo.get_all({'name': '0'})]
    assert obj_pk[0] == objects[0].pk
    obj_pk = [obj.pk for obj in repo.get_all({'parent': '897'})]
    assert obj_pk == [o.pk for o in objects]

    for o in objects:
        repo.delete(o.pk)


def test_get_like_without_where():
    with pytest.raises(ValueError):
        repo.get_like()


def test_get_like():
    objects = []
    for i in range(5):
        o = Category('', 2)
        o.name = str(i)
        o.parent = 897
        repo.add(o)
        objects.append(o)
    obj_pk = [obj.pk for obj in repo.get_like({'name': '0'})]
    assert obj_pk[0] == objects[0].pk
    obj_pk = [obj.pk for obj in repo.get_like({'parent': '89%'})]
    assert obj_pk == [o.pk for o in objects]

    for o in objects:
        repo.delete(o.pk)


