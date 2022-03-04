from rest_framework import serializers
from job_seeker.models import EducationDetail, ExperienceDetail, SkillSet, Profile
from skill.models import Skill


class EducationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationDetail
        exclude = ['profile', 'id']


class ExperienceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceDetail
        exclude = ['profile', 'id']


class SkillSetSerializer(serializers.ModelSerializer):
    skill_name = serializers.StringRelatedField(source='skill_set.skill_name')
    class Meta:
        model = SkillSet
        exclude = ['profile', 'id']


class ProfileSerializer(serializers.ModelSerializer):
    education = EducationDetailSerializer(many=True)
    experience = ExperienceDetailSerializer(many=True)
    skill = SkillSetSerializer(many=True)

    class Meta:
        model = Profile
        exclude = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        education = validated_data.pop("education")
        experience = validated_data.pop("experience")
        skill = validated_data.pop("skill")
        profile = Profile.objects.create(user=user, **validated_data)
        
        for each in education:
            EducationDetail.objects.create(profile=profile, **each)

        for each in experience:
            ExperienceDetail.objects.create(profile=profile, **each)

        for each in skill:
            SkillSet.objects.create(profile=profile, **each)
        return profile

    def update(self, instance, validated_data):
        # popping some values
        education = validated_data.pop("education")
        experience = validated_data.pop("experience")
        skill = validated_data.pop("skill")

        # updating instance
        profile = instance
        for key, value in validated_data.items():
            setattr(profile, key, value)
        profile.save()

        # deleting old values
        profile.education.all().delete()
        profile.experience.all().delete()
        profile.skill.all().delete()

        # updating pop items
        for each in education:
            education.objects.create(profile=profile, **each)

        for each in experience:
            experience.objects.create(profile=profile, **each)

        for each in skill:
            skill.objects.create(profile=profile, **each)

        return profile