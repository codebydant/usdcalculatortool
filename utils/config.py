from omegaconf import OmegaConf, DictConfig


def load_config() -> DictConfig:
    config = OmegaConf.load("common.yaml")
    config = OmegaConf.to_container(config, resolve=True)
    config = OmegaConf.create(config)
    return config
