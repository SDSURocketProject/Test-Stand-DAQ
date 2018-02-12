# SDSU Rocket Project Contribution Guide

### PR Standards

Create a new branch and PR for each issue addressed. 

This allows us to accept/reject PRs on a feature-by-feature basis without having a reject a feature only because it is in the same PR as something we do not want.  

The name of your PR should be short and descriptive of the issue your branch addresses.

### How to Contribute
- Select an issue to work on from the list [here](https://github.com/SDSURocketProject/Test-Stand-DAQ/issues)

- Clone the repo to your local computer. 
	```
	git clone https://github.com/SDSURocketProject/Test-Stand-DAQ.git
	```
- Create a new branch with a name that describes the issue you're working on.
	```
	git branch <branchname>
	```

- Switch to the branch you created and start working on issue. 
	```
	git checkout <branchname>
	```

- Ensure to periodically commit and push changes to your local repository to save your work to the online git repository.
	``` 
	git add <filename(s)>
	git commit -m <message>
	git push origin <branchname>
	```

- When you're finished making changes to your branch, submit a new pull request to merge your branch into master [here](https://github.com/SDSURocketProject/Test-Stand-DAQ/pulls)

- Ensure your pull request is approved by a reviewer, usually someone related to the content of your PR, then merge the branch with master and delete your old branch.

# Glossary
- Issues
	- A running ToDo list of fixes and additions to the software in this repository. If you want to get started making contributions, this is the place to start.

- Pull Request
	- A request to pull commits from one branch (or fork) to another branch.
	- Pull requests address issues, and should merge a new branch created to fix an issue, with the master branch.

- Branch
	- A branch is safe a way to introduce changes to a repository. A branch is a clone of the main repository that can be later merged with the master branch or deleted.

	- The master branch is the main current version of the repository. All branches should eventually be deleted or merged with the master branch.

- Fork
	- A fork is a clone of the main repository to your personal git hub account.
	- Working in a fork rather than a branch prevents unnecessary clutter in the base repo.
	- Forks are NOT for contributions or fixing issues, but to introduce major changes and more personal projects and experiments.

- .gitignore
	- This file is used to specify what will be staged for commit automatically when executing the `git add` or `git add -A` commands. For example, adding "stuff/" to the .gitignore file will ignore and NOT stage any folders labled 'stuff/'
