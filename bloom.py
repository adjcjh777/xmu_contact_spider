from pybloom_live import ScalableBloomFilter ,BloomFilter

# 初始化定长和可伸缩的bloom
def init_scale_bloom(size=1e8):
    scalable_bloom = ScalableBloomFilter(initial_capacity=size)
    return scalable_bloom


def init_static_bloom(size=1e8):
    static_bloom = BloomFilter(capacity=size)
    return static_bloom
