from pytest import File, Item

class JsonFile(File):
    def collect(self):
        # We need a json parser
        import json

        raw = json.load(self.path.open(encoding="utf-8"))
        yield PackMetadataAuthor.from_parent(self, name=f"Pipeline Tags", json=raw)
        yield PackMetadataDescription.from_parent(self, name=f"Pipeline Name", json=raw)

class JsonItem(Item):
    def __init__(self, *, json, **kwargs):
        super().__init__(**kwargs)
        self.json = json

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, JsonException):
            return "\n".join(excinfo.value.args)
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.path, 0, f"{self.name}: {str(self.path).replace(f"{str(self.config.rootdir)}/", '')}"


class PackMetadataAuthor(JsonItem):
    def runtest(self):
        if len(self.json.get('author', '')) == 0:
            raise JsonException("* No Author defined *", "All packs must have an author defined")
        
class PackMetadataDescription(JsonItem):
    def runtest(self):
        if len(self.json.get('description', '')) == 0:
            raise JsonException("* No Description defined *", "All packs must have a description defined")

class JsonException(Exception):
    """Custom exception for error reporting."""
