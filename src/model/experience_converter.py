class ExperienceConverter(object):
    @staticmethod
    def experience_to_new_level(current_level, current_experience):
        return max(30 * current_level - current_experience, 0)
