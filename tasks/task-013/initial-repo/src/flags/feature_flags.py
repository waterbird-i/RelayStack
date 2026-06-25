def is_enabled(flags, name, default=False, env=None):
    env = env or {}
    env_key = "FEATURE_" + name.upper()
    value = env.get(env_key) or flags.get(name) or default
    return bool(value)
