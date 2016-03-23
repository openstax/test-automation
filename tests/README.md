# To get up and running

## Get this code

```bash
git clone git@github.com:openstax/test-automation.git
cd test-automation
git checkout spike/tutor
```

We are now in the version of `test-automation` where you can start writing tests.

## Install

We will need `node v0.12.10` to get running.  `nvm` will help you install `node` and have different versions of `node` available.  Follow the ["Install Script" instructions from here](https://github.com/creationix/nvm#install-script).

Then,

```bash
nvm install 0.12.10
npm install -g npm@latest
```

Finally, we need to install the packages for this set of code:

```bash
npm install
```

This will tell `npm` -- [node package manager](https://docs.npmjs.com/getting-started/what-is-npm) -- to look at our [`package.json`](../package.json) file in the project we are `cd`ed into -- `test-automation` and install the necessary packages.

## Example usage

Now, we are ready to run.  To check that tests are working, try:

```bash
npm test -- --c 7612
```

If all has gone well, you should see two browsers open on your computer -- one Chrome, one Firefox -- driven with test actions.

We've told it to run [this test case](./tutor/teacher-views.coffee#L64-L84).

You can run

```bash
npm test -- -h
```
to get information about all options for the `npm test` command.

For example,

```bash
npm test -- --settings stax-attack.json --r sauce
```

will run the cases set as options in [`stax-attack.json`](../stax-attack.json), and any added options from the commandline, the "sauce" remote in this case.

The credentials for the remotes can be defined as `environment` variables when you're calling the command or in a file named `.env`.  The `.env` file should follow the [`.env.example`](../.env.example) file in the root of this project.

## To write new cases

You can follow the pattern of the current tests in the files in [`tutor`](./tutor).  For new test sections that don't have a file to correspond with yet, you can create a new file.  To learn more about using the test `Helpers`, check out [this](https://github.com/openstax/tutor-js/tree/master/test-integration/helpers) and [this](http://openstax.github.io/tutor-js/docs/).  These docs are very much works in progress :cry:.  Sorry.


Underneath, the tests are running with `mocha`, `chai`, and `selenium`.  It will help to get familiar with these dependencies as you write new test cases.
