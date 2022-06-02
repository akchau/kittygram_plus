from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
# import webcolors
import datetime as dt


from .models import Achievement, Cat, AchievementCat, CHOICES, User # Owner

'''
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
'''
class UserSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'cats')
        ref_name = 'ReadOnlyUsers'


class AchievementSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Achivement."""
    # переименовали поле сериализвтора и указали источник
    # настоящее название поля name
    achivement_name = serializers.CharField(source='name')
    class Meta:
        model = Achievement
        fields = ('id', 'achivement_name')


'''
class CatListSerializer(serializers.ModelSerializer):
    """Дополнительный сериализатор для модели Cats"""
    color = serializers.ChoiceField(choices=CHOICES)
    
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')
'''

class CatSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Cat."""
    # owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    color = serializers.ChoiceField(choices=CHOICES)
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements', 'age')
        # read_only_fields = ('owner',)
        validators = [
            UniqueTogetherValidator(
                queryset=Cat.objects.all(),
                fields = ('name', 'owner'),
                message = 'У вас уже есть такой котик'
            )
        ]

    def validate_birth_year(self, value):
        "Валидация года на уровне сериализатора."
        year = dt.date.today().year
        if not (year - 40 < value <= year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value

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

    def validate(self, data):
        """Проверка совпадения имени и цвета
        Проверка на уровне объекта модели."""
        if data['color'] == data['name']:
            raise serializers.ValidationError(
                'Имя не может совпадать с цветом'
            )
        return data
        


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

'''
class OwnerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели владельца."""
    cats = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
'''