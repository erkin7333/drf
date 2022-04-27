from rest_framework import serializers
from .models import Kino, Review, Reyting, Actyor



class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class AktyorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actyor
        fields = ['id', 'name', 'image']


class AktyorDetaileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actyor
        fields = "__all__"


class KinoListSerializer(serializers.ModelSerializer):
    reting_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()
    class Meta:
        model = Kino
        fields = ['id', 'title', "tagline", "category", "reting_user", "middle_star"]

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children",)


class KinoDetailSerializer(serializers.ModelSerializer):
# Detail serializerda Kino modelga ulanga Quyidagilarni nominii list ko'rinishda chiqarish
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = AktyorListSerializer(read_only=True, many=True)
    actors = AktyorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Kino
        exclude = ("draft",)


class CreateReytingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reyting
        fields = ['star', 'movie']

    def create(self, validated_data):
        reting, _ = Reyting.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return reting

