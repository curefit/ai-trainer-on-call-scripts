import csv
import json

import aiohttp
import asyncio
import time


def get_user_ids(user_ids_filename):
    with open(user_ids_filename) as f:
        user_ids = list(csv.reader(f, delimiter=','))[1:]
    return user_ids


def get_plan_maps(plan_maps_filename):
    with open(plan_maps_filename) as f:
        plan_maps = list(csv.reader(f, delimiter=','))[1:]
    return plan_maps


async def sync_plan(session, request_body):
    url = "http://user-fitness-service.production.cure.fit.internal/sync/managed_microcycle_single_user"
    headers = {'Content-type': 'application/json'}

    async with session.put(url, data=json.dumps(request_body), headers=headers) as res:
        status = await res.text()
        print(status)


async def sync_all_plans(user_ids_filename, plan_maps_filename):
    user_ids_rows = get_user_ids(user_ids_filename)
    plan_maps_rows = get_plan_maps(plan_maps_filename)

    request_bodies = []
    for plan_maps_row in plan_maps_rows:
        for user_ids_row in user_ids_rows:
            old_managed_micro_cycle_id = plan_maps_row[0]
            new_managed_micro_cycle_id = plan_maps_row[1]
            user_id = user_ids_row[0]
            request_bodies.append({
                'userId': user_id,
                'oldManagedMicrocycleId': old_managed_micro_cycle_id,
                'newManagedMicrocycleId': new_managed_micro_cycle_id
            })

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=5)) as session:
        tasks = []

        for request_body in request_bodies:
            tasks.append(asyncio.ensure_future(sync_plan(session, request_body)))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    # asyncio.run(sync_all_plans(user_ids_filename='test_user_ids.csv', plan_maps_filename='test_plan_maps.csv'))
    asyncio.run(sync_all_plans(user_ids_filename='user_ids.csv', plan_maps_filename='plan_maps.csv'))
    print("--- %s seconds ---" % (time.time() - start_time))
