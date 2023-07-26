import requests

def get_followers(username, access_token):
    headers = {
        "Authorization": f"token {access_token}"
    }
    followers_url = f"https://api.github.com/users/{username}/followers"
    followers = set()
    page = 1
    while True:
        params = {
            "page": page,
            "per_page": 100
        }
        response = requests.get(followers_url, headers=headers, params=params)
        if response.ok:
            followers_data = response.json()
            if not followers_data:
                break
            for follower in followers_data:
                followers.add(follower["login"])
            page += 1
        else:
            break
    return followers

def get_following(username, access_token):
    headers = {
        "Authorization": f"token {access_token}"
    }
    following_url = f"https://api.github.com/users/{username}/following"
    following = set()
    page = 1
    while True:
        params = {
            "page": page,
            "per_page": 100
        }
        response = requests.get(following_url, headers=headers, params=params)
        if response.ok:
            following_data = response.json()
            if not following_data:
                break
            for user in following_data:
                following.add(user["login"])
            page += 1
        else:
            break
    return following

def unfollow_user(username_to_unfollow, access_token):
    unfollow_url = f"https://api.github.com/user/following/{username_to_unfollow}"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.delete(unfollow_url, headers=headers)
    return response.ok

def main():
    your_username = "YOUR_USERNAME"
    your_access_token = "YOUR_ACCESS_TOKEN"

    your_followers = get_followers(your_username, your_access_token)
    your_following = get_following(your_username, your_access_token)

    not_following_back = your_following - your_followers

    print("Sizi geri takip etmeyen kullanıcılar:")
    for user in not_following_back:
        print(user)

    for user_to_unfollow in not_following_back:
        success = unfollow_user(user_to_unfollow, your_access_token)
        if success:
            print(f"Unfollowed: {user_to_unfollow}")
        else:
            print(f"Failed to unfollow: {user_to_unfollow}")

if __name__ == "__main__":
    main()
