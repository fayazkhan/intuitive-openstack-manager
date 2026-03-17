from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration.

    This uses Pydantic's BaseSettings to allow overriding values via ENV variables.
    """

    # Backend selection: 'mock' is a lightweight in-memory implementation suitable for
    # local development and demos. A real OpenStack-backed implementation can be
    # provided in the future.
    openstack_backend: str = "mock"

    # (Optional) OpenStack auth configuration (used by a real backend)
    openstack_auth_url: str = ""
    openstack_project_name: str = ""
    openstack_username: str = ""
    openstack_password: str = ""
    openstack_user_domain_name: str = "Default"
    openstack_project_domain_name: str = "Default"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
