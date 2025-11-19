Development is facilitated via VS Code dev. environments. To try out our development environment, clone the repository, open VS Code and enter de dev. container mode:

![Cybersentry Development Environment](media/cai_devenv.gif)


### Contributions

If you want to contribute to this project, use [**Pre-commit**](https://pre-commit.com/) before your MR

```bash
pip install pre-commit
pre-commit # files staged
pre-commit run --all-files # all files
```

### Optional Requirements: caiextensions

Currently, the extensions are not available as they have been (largely) integrated or are in the process of being integrated into the core architecture. We aim to have everything converge in version 0.4.x. Coming soon!

### Usage Data Collection

Cybersentry is provided free of charge for researchers. To improve Cybersentry’s detection accuracy and publish open security research, instead of payment for research use cases, we ask you to contribute to the Cybersentry community by allowing usage data collection. This data helps us identify areas for improvement, understand how the framework is being used, and prioritize new features. Legal basis of data collection is under Art. 6 (1)(f) GDPR — Cybersentry’s legitimate interest in maintaining and improving security tooling, with Art. 89 safeguards for research. The collected data includes:

- Basic system information (OS type, Python version)
- Username and IP information
- Tool usage patterns and performance metrics
- Model interactions and token usage statistics

We take your privacy seriously and only collect what's needed to make Cybersentry better. For further info, reach out to research＠cybe4sent1nel(FAHAD KHAN).com. You can disable some of the data collection features via the `Cybersentry_TELEMETRY` environment variable but we encourage you to keep it enabled and contribute back to research:

```bash
Cybersentry_TELEMETRY=False cai
```

### Reproduce CI-Setup locally

To simulate the CI/CD pipeline, you can run the following in the Gitlab runner machines:

```bash
docker run --rm -it \
  --privileged \
  --network=exploitflow_net \
  --add-host="host.docker.internal:host-gateway" \
  -v /cache:/cache \
  -v /var/run/docker.sock:/var/run/docker.sock:rw \
  registry.gitlab.com/cybe4sent1nel(FAHAD KHAN)/alias_research/cai:latest bash
```