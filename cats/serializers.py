from rest_framework import serializers
import webcolors
import datetime as dt


from .models import Achievement, Cat, Owner, AchievementCat, CHOICES


class Hex2NameColor(serializers.Field):
    """Класс который по коду цвета возвращает его название."""
    def to_representation(self, value):
        return value
    
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Achivement."""
    achivement_name = serializers.CharField(source='name')
    class Meta:
        model = Achievement
        fields = ('id', 'achivement_name')



class CatListSerializer(serializers.ModelSerializer):
    """Дополнительный сериализатор для модели Cats"""
    color = serializers.ChoiceField(choices=CHOICES)
    
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')


class CatSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Cat."""
    # owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    color = serializers.ChoiceField(choices=CHOICES)
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements', 'age')
    
    def create(self, validated_data):
        """Метод для добавления достижений котика, если они переданы вместе с post-запросом."""
        if 'achievements' not in self.initial_data:
            # То создаём запись о котике без его достижений
            cat = Cat.objects.create(**validated_data)
            return cat
        achievements = validated_data.pop('achievements')
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(**achievement)
            AchievementCat.objects.create(achievement=current_achievement, cat=cat)
        return cat

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year 
"""
    def update(self, validated_data):
        achievements = validated_data.pop('achievements')
        cat = Cat.objects.filter(id=self.initial_data['id']).update(**validated_data)
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(**achievement)
            AchievementCat.objects.create(achievement=current_achievement, cat=cat)
        return cat
"""


class OwnerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели владельца."""
    cats = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
