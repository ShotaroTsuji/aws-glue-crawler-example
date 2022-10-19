from abc import ABC, abstractmethod

from aws_cdk.aws_s3_deployment import Source, ISource


class DataSet(ABC):

    @property
    @abstractmethod
    def prefix(self) -> str:
        pass

    @property
    @abstractmethod
    def sources(self) -> list[ISource]:
        pass


class JsonDataExample(DataSet):

    @property
    def prefix(self) -> str:
        return "json-data-example"

    @property
    def sources(self) -> list[ISource]:
        return [
            Source.json_data('/year=2022/month=08/01.json', {"id": "20220801"})
        ]


class FlatAndOneCommonKey(DataSet):

    @property
    def prefix(self) -> str:
        return "flat-and-one-common-key"

    @property
    def sources(self) -> list[ISource]:
        return [
            Source.json_data(f'/{i}.json', {
                "id": str(i),
                f"key{i}": str(i)
            }) for i in range(0, 30)
        ]


class DisjointKeys(DataSet):

    @property
    def prefix(self) -> str:
        return "disjoint-keys"

    @property
    def sources(self) -> list[ISource]:
        return [
            Source.json_data(f'/year=2022/month={m:02}/{d:02}.json',
                             {f"key{d:02}": d}) for d in range(1, 3)
            for m in range(1, 13)
        ]


class NonHiveDisjointKeys(DataSet):

    @property
    def prefix(self) -> str:
        return "non-hive-disjoint-keys"

    @property
    def sources(self) -> list[ISource]:
        return [
            Source.json_data(f'/2022/{m:02}/{d:02}.json', {f"key{d:02}": d})
            for d in range(1, 3) for m in range(1, 13, 2)
        ]


class OverlappingKeys(DataSet):

    @property
    def prefix(self) -> str:
        return "overlapping-keys"

    @property
    def sources(self) -> list[ISource]:
        return [
            Source.json_data(f'/year=2022/month={m:02}/{d:02}.json', {
                "id": 10 * m + d,
                "description": f"json of {m}/{d}",
                f"q{d%2}": d
            }) for d in range(1, 3) for m in range(1, 13, 2)
        ]
