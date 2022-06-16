import random
import os
import time
from typing import Any, Dict, List

random.seed(1)

resource_ids: List[int] = random.sample(range(1, 31), random.randint(1, 30))
users: List[int] = random.sample(range(1, 31), random.randint(1, 30))

resources: List[Dict[str, Any]] = [
    {
        'id': id,
        'tasks': []
    } for id in resource_ids
]
"""
[
    {
        "id": <resource_id>,
        "tasks": [
            "user": <user_id>,
            "time": ...,
        ]
    }
]
"""


def find_resource(resource_id: int):
    return resource_ids.index(resource_id)


def sort_users():
    for index, resource in enumerate(resources):
        resources[index]['tasks'] = sorted(
            resource['tasks'], key=lambda r: r['user'], reverse=True)


def remove_user(user_id: int):
    users.remove(user_id)


def calculate_total_time(tasks: List[Dict[str, Any]]):
    return sum([task['time'] for task in tasks])


def add_tasks(resource_ids: List[int], user_id: int):
    _ = [
        resources[find_resource(resource_id)]['tasks'].append({
            "user": user_id,
            "time": random.randint(1, 30),
        }) for resource_id in resource_ids
    ]

    sort_users()
    remove_user(user_id)


def allocate():
    user: int = 0
    while True:
        try:
            os.system('clear')
            user = int(input(
                f"""
####################################################################
                Allocating a given user
        
        Available users: {users}

        Note: Input 0 to cancel

        Input user: """
            ))
            break
        except Exception:
            pass

    if not user:
        return

    add_tasks(random.sample(resource_ids,
              random.randint(1, len(resource_ids))), user)


def resource_manager():
    os.system('clear')
    print(
        """
####################################################################
                        Resource Manager
        
            {:<15} {:<15} {:<15} {:<15}
    """.format('Resource', 'Current User', 'Time Left', 'Free In')
    )
    _ = [
        print(
            """
            {:<15} {:<15} {:<15} {:<15}""".format(resource['id'], resource['tasks'][0]['user'], resource['tasks'][0]['time'], calculate_total_time(resource['tasks']))
        )
        if len(resource['tasks'])
        else
        print(
            """
            {:<15} {:<15} {:<15} {:<15}""".format(resource['id'], 'None', 0, 0)
        )
        for resource in resources

    ]
    time.sleep(3)


def resource_waitlist():
    os.system('clear')
    print(
        """
####################################################################
                        Waitlisted Users
        
            {:<15} {:<15} {:<15}
    """.format('User', 'Resource', 'Starts At')
    )
    _ = [
        [
            print(
                """
            {:<15} {:<15} {:<15}""".format(task['user'], resource['id'], calculate_total_time(resource['tasks'][:index]))
            )
            for index, task in enumerate(resource['tasks'])
            if index > 0
        ]
        for resource in resources
        if len(resource['tasks']) > 1
    ]
    time.sleep(3)


def timeskip():
    timeskip: int = 0
    while True:
        try:
            os.system('clear')
            timeskip = int(input(
                f"""
####################################################################
                Commencing timeskip

        Note: Input 0 to cancel

        Input timeskip value (in seconds): """
            ))
            break
        except Exception:
            pass

    if not timeskip:
        return

    for i, resource in enumerate(resources):
        current_timeskip = timeskip
        while len(resource['tasks']) > 0:
            if resource['tasks'][0]['time'] - current_timeskip <= 0:
                current_timeskip -= resource['tasks'][0]['time']
                resources[i]['tasks'].pop(0)
            else:
                resource['tasks'][0]['time'] -= current_timeskip
                break


def main():
    while True:
        os.system('clear')
        command: str = (input(
            """
####################################################################
                Time-sharing System Simulation
        
        Commands:
        
            1.  Allocate resource for user
            2.  Display resource manager
            3.  Display resource waitlist
            4.  Perform timeskip

####################################################################

        Input: """
        ))

        if command == '1':
            allocate()
        elif command == '2':
            resource_manager()
        elif command == '3':
            resource_waitlist()
        elif command == '4':
            timeskip()
        else:
            break


if __name__ == '__main__':
    main()
