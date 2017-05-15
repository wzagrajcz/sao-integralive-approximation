import sys
import random
import operator


class ProbabilityDistribution:
    def __init__(self, source_map, alpha = 1):
        self.source_map = source_map

        min_value = sys.float_info.max
        max_value = sys.float_info.min
        for midpoint, improvement in source_map.iteritems():
            if min_value > improvement:
                min_value = improvement
            if max_value < improvement:
                max_value = improvement

        offset = alpha - min_value
        normalizer = 0.01 * (max_value + offset)
        normalized_map = {}

        for midpoint, improvement in source_map.iteritems():
            normalized_map[midpoint] = (improvement + offset) / normalizer

        self.normalized_map = normalized_map

        self.probability_map = {}
        sum = 0

        for (k, v) in normalized_map.iteritems():
            sum += v

        for (k, v) in normalized_map.iteritems():
            self.probability_map[k] = v/sum

        self.probability = sorted(self.probability_map.items(), key=operator.itemgetter(0))

    def get_random_element(self):
        midpoint_to_endrange = {}

        range_builder = 0
        for midpoint, improvement in self.normalized_map.iteritems():
            range_builder += improvement
            midpoint_to_endrange[midpoint] = range_builder

        picked_number = random.random() * range_builder

        highest_lower_then_value = sys.float_info.min
        highest_lower_then_key = None

        for midpoint, end_of_range in midpoint_to_endrange.iteritems():
            if picked_number <= end_of_range and highest_lower_then_value < end_of_range:
                highest_lower_then_key = midpoint

        self.normalized_map.pop(highest_lower_then_key)
        return highest_lower_then_key
