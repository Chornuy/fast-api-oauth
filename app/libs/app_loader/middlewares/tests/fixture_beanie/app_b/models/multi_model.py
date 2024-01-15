from beanie import Document, UnionDoc


class Parent(UnionDoc):  # Union
    class Settings:
        name = "union_doc_collection"  # Collection name
        class_id = "_class_id"  # _class_id is default beanie internal field used to filter children Documents


class One(Document):
    int_field: int = 0
    shared: int = 0

    class Settings:
        name = "One"  # Name used to filer union document 'One', default to class name
        union_doc = Parent


class Two(Document):
    str_field: str = "test"
    shared: int = 0

    class Settings:
        union_doc = Parent
