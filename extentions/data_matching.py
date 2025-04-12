from account.models import UserSkillProfile


def find_matches_for_user(user):
    if not hasattr(user, 'skill_profile'):
        return []

    user_profile = user.skill_profile

    # user offers
    offered_skills = user_profile.offers.all()

    # user demands
    demanded_skills = user_profile.demands.all()

    # demand match
    demand_matches = UserSkillProfile.objects.filter(
        demands__in=offered_skills
    ).exclude(user=user).distinct()

    # offer match
    offer_matches = UserSkillProfile.objects.filter(
        offers__in=demanded_skills
    ).exclude(user=user).distinct()

    return {
        'offers_for_user': offer_matches,
        'demands_for_user': demand_matches
    }
