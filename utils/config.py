from omegaconf import OmegaConf


def load_config():
    config = OmegaConf.load("common.yaml")
    config = OmegaConf.to_container(config, resolve=True)
    config = OmegaConf.create(config)
    return config
