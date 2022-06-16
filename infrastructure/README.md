# Infrastructure as Code of policy-management-service

Treat this folder as a sub project itself. This is the project that can deploy the other projects in the repository in an automated way using AWS CDK.

## Getting started

The next workflow has been tested on Linux.
Treat this folder as a sub project itself, so, open it.
```bash
cd infrastructure
```

### Global dependencies

You need:
* AWS CLI
* Python3
* AWS CDK

Install AWS CDK with
```bash
sudo npm install -g aws-cdk
```

### Configuration

You need to install AWS CLI. Then, use this command to set up the credentials of your AWS account.
```bash
aws configure
```

You also can configure your aws credentials editing this file:
```
nano ~/.aws/credentials
```

### Local dependencies

Create a virtualenv on MacOS and Linux:

```bash
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```bash
source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```bash
pip install -r requirements.txt
```

At this point you can now list the CloudFormation Stacks for this code.

```bash
cdk list
```

### Deploy

List your stacks
```bash
cdk list
```

Then, pick the name of the stack that you want to deploy and:
```bash
cdk deploy stack0 stack1 ...
```

### Delete CloudFormation Stacks

```bash
cdk destroy --all
# Or:
cdk destroy <stackname>
```

Some information won't be deleted in this process.
Read more about it in (this issue)[https://github.com/aws/aws-cdk-rfcs/issues/64].

## Troubleshooting

### Can't deploy because certificate isn't created

This could be because you have to configure the namespaces of your domain.
Follow the next steps:
1. Run `cdk deploy`.
2. Wait until your CDK creates the Hosted Zone.
3. Log in in AWS Console and go to your hosted zones.
4. Go to the hosted zone that CDK created.
5. You'll see four namespaces in the column `Value/Route traffic to`.
6. Copy each one and go to your domain provider, (for instance domain.com).
7. Select your domain y go to its configuration.
8. Find some "namespaces" list.
9. Paste the copied namespaces that you copied in the step 5.
10. Save it.
11. Wait until the command `cdk deploy` finishes, this takes like 15 minutes.

### Can't delete the stack with cdk destroy

Maybe this is because you have to delete your Hosted Zone manually. 
This seems to be an issue: https://github.com/aws/aws-cdk/issues/4155

### Some assets aren't deleted by cdk destroy

If you run `cdk destroy --all`, some information won't be deleted.
Read more about it in this issue: https://github.com/aws/aws-cdk/issues/7194

### State cannot be updated

If you ran `cdk deploy`, and some stack can't be updated, you may move the state of your stack by using AWS CLI.
Here, some useful commmands:

* `aws cloudformation delete-stack --stack <stackname>` delete a stack
* `aws cloudformation cancel-update-stack --stack <stackname>` cancel a stack update
* `aws cloudformation list-stacks` list real remote stacks of the account

### Error UtilConnectToInteropServer

I got this error using the terminal of Visual Studio. Try using another terminal.

## Important commands

* `aws configure`   global configuration about your aws account and region
* `cdk ls`          list all stacks written in the code
* `cdk diff`        compare deployed stack with current state
* `python3 build.py`build some stuff in order to deploy
* `cdk deploy`      deploy this stack to your default AWS account/region

## Miscellaneous

If you don't want to install AWS CDK globally, you still can using it with "npx" like so:
```bash
npx aws-cdk <subcommand>
```

In order to create this project, AWS CDK version 2.1.0 has been used.

If you deploy this, you'll see an AWS Cloudformation Stack called CDKToolkit listed. Don't worry about it, CDK created that for its purpose.

The `cdk.json` file tells the CDK Toolkit how to execute your app.
