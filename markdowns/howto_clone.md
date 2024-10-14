# How to clone the repo

It is a private repository at this time. It will be public when I am done playing around with it. Here are the steps to clone it over https. Only collaborators can access the repo.
You must obtain a Access Token first in order to clone the repo.

Please look at information on how to clone a private repository at: https://docs.github.com/en/repositories/creating-and-managing-repositories/troubleshooting-cloning-errors

You can clone the repo using either HTTPS or SSH.

## Cloning the repo over HTTPS

- Click on the profile at the upper right corner
- Click on **Settings**
- Click on **Developer Settings** all the way at the bottom
- Click on **Personal access tokens**
- Tokens classic
- Generate a classic token
- Copy it, store it, you won’t be able to see it again
- Now clone the repo over https, add the access token after https.
- git clone https://your_access_token@github.com/muquit/privategpt.git
- `cd privategpt`
## Cloning the repo over SSH

- Start the ssh-agent:
   ```bash
   eval "$(ssh-agent -s)"
   ```
- Add your SSH private key:

   * If you don't have one, generate it:

     ```bash
     ssh-keygen -t ed25519 -C "your_email@example.com"
     ```

   * Add the key to the agent:

     ```bash
     ssh-add ~/.ssh/id_ed25519
     ```

- Add your public key to GitHub:

   * Copy your public key:
     ```bash
     cat ~/.ssh/id_ed25519.pub
     ```
        Example:
        ```bash
        ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOJki52OW/dkcEkMuRGFV8ClW3T8pCqrwly79NzhxgnF your_email@example.com
        ```
   * Go to GitHub settings > SSH and GPG keys.
   * Click "New SSH key" or "Add SSH key".
   * Paste your key, give it a title, and click "Add SSH key".

- You can now use SSH to interact with GitHub and clone the repo without entering your password.
     ```bash
     git clone git@github.com:muquit/privategpt.git
     ```
     ```

- Notes:
     * The `ssh-agent` keeps your key in memory until it's restarted.
     * Consider setting up `ssh-agent` to start automatically on login.
     * Make sure your key permissions are correct (`chmod 600 ~/.ssh/id_ed25519`). 