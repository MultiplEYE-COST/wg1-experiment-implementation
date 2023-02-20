# Contributing to the implementation of the experimental presentation of MultiplEYE
Thank you for taking your time to contribute to the implementation of the experimental presentation of MultiplEYE!

We encourage you to report any bugs or contribute to new features, optimisations or documentation.

Here we give you an overview of the workflow and best practices for contributing.

**Questions:** If you have any developer-related questions, please contact Deborah on slack.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Reporting Bugs](#reporting-bugs)
- [First-time Contributors](#first-time-contributors)
- [Getting Started](#getting-started)
  - [Development Installation](#development-installation)
  - [Creating a Branch](#creating-a-branch)
  - [Code Style](#code-style)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Pull Requests](#pull-requests)
  - [Continuous Integration](#continuous-integration)
- [Core Developer Guidelines](#core-developer-guidelines)
- [License](#license)
- [Questions](#questions)


## Code of Conduct

Everyone contributing to this code base, and in particular in our issue tracker and pull
requests, is expected to treat other people with respect and more generally to follow the guidelines
articulated in the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).


## Reporting Bugs

If you discover a bug, as a first step please check the existing
[Issues](https://github.com/aeye-lab/pymovements/issues) to see if this bug has already been
reported.

In case the bug has not been reported yet, please do the following:

- [Open an issue](https://github.com/aeye-lab/pymovements/issues/new?labels=bug&template=ISSUE.md).
- Add a descriptive title to the issue and write a short summary of the problem.
- We provide you with a default template to guide you through a typical reporting process.
- Adding more context, including error messages and references to the problematic parts of the code,
would be very helpful to us.

Once a bug is reported, our development team will try to address the issue as quickly as possible.

## Getting Started

This is a general guide to contributing changes to the experimental presentation.

### Creating a Branch

Before you start making changes to the code, create a local branch from the latest version of the
`main` branch.

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-branch
```

We do not allow for pushing directly to the `main` branch and merge changes exclusively by
[pull requests](#pull-requests).

We will squash your commits into a single commit on merge to maintain a clean git history.
We use a linear git-history, where each commit contains a full feature/bug fix, such that each
commit represents an executable version. This way you also don't have to worry much about your
intermediate commits and can focus on getting your work done first.


### Code Style

We write our code to follow [PEP-8](https://www.python.org/dev/peps/pep-0008) with a maximum
line-width of 100 characters. We additionally use type annotations as in [PEP-484](
https://peps.python.org/pep-0484). For docstrings we use the [numpydoc](
https://numpydoc.readthedocs.io/en/latest/format.html) formatting standard.

### Testing

It is probably not possible to write meaningful unittests for the implementation. For certain methods or classes
it might be possible but not for all. Therefore:

- please make sure you test your code at least by running the dummy experiment or if possible with an actual eye-tracker
- if there are methods where you think it is possible to add unittests, please do so


### Pull Requests

Once you are ready to publish your changes:

- Create a [pull request (PR)](https://github.com/aeye-lab/pymovements/compare).
- Provide a summary of the changes you are introducing according to the default template.
- In case you are resolving an issue, don't forget to add a reference in the description.

The default template is meant as a helper and should guide you through the process of creating a
pull request. It's also totally fine to submit work in progress, in which case you'll likely be
asked to make some further changes.

If your change will be a significant amount of work to write, we highly recommend starting by
opening an issue laying out what you want to do. That lets a conversation happen early in case other
contributors disagree with what you'd like to do or have ideas that will help you do it.

The best pull requests are focused, clearly describe what they're for and why they're correct, and
contain tests for whatever changes they make to the code's behavior. As a bonus these are easiest
for someone to review, which helps your pull request get merged quickly. Standard advice about good
pull requests for open-source projects applies.

Do not squash your commits after you have submitted a pull request, as this
erases context during review. We will squash commits when the pull request is ready to be merged.


