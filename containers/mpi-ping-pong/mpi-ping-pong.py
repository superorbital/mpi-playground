#!/usr/bin/env python

# Based on examples from:
# https://pdc-support.github.io/introduction-to-mpi/aio/index.html
#
# But expanded to be more verbose and work in more use cases.

from mpi4py import MPI

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()
rrank = rank + 1

# Introduce ourselves
print("Hello, World! I am 🏓 Player (Rank) ", rank, ". Process ", rrank ," of ",size," on ",name, flush=True)

max_count = 300 * size
ball = 1

# Find the neighbor we receive the ball from and the neighbor we send the ball to.
if rank == 0:
    if size == 1:
        rn = 0
        sn = 0
    else:
        rn = size - 1
        sn = rank + 1
elif rank != 0 and rrank == size:
        rn = rank - 1
        sn = 0
else:
    rn = rank - 1
    sn = rank + 1

# Announce who our neighbors are
print("Player (Rank) ", rank, "'s receiving 🏓 neighbor is Player (Rank) {:d} and my sending 🏓 neighbor is Player (Rank) {:d}.".format(rn,sn), flush=True)

# Tracking the counter is not a great method here since we have messaging, but it works...
if rank == 0:
    counter = 1
else:
    counter = 0

# If we are Rank 0, we get to start the match.
if rank == 0:
    # Rank 0 starts with the ball
    req = MPI.COMM_WORLD.isend(ball, dest=sn, tag=0)
    if size == 1:
        print("Player {:d} started round {:d} by hitting the 🏓 ball towards the wall.".format(rank,counter), flush=True)
    else:
        print("Player {:d} sent the 🏓 ball to Player {:d}.".format(rank,sn), flush=True)

bored = False
last = False

# Now run a send and receive in a loop until someone gets bored
while not bored:
    if counter <= max_count:
        # Receive the ball
        req = MPI.COMM_WORLD.irecv(source=rn, tag=0)
        recv_message = req.wait()
        if size == 1:
            print("Player {:d} received the 🏓 ball that bounced off the wall.".format(rank), flush=True)
        else:
            print("Player {:d} received the 🏓 ball from Player {:d}.".format(rank,rn), flush=True)

    # Increment the counter and send the ball
    counter += 1

    # We don't want to send a ball once we are done playing for the moment.
    if counter <= max_count:
        # Determine if we are the last player standing.
        if (rrank == size) and (counter == max_count):
            last = True
        else:
            req = MPI.COMM_WORLD.isend(ball, dest=sn, tag=0)
            if size == 1:
                print("Player {:d} started round {:d} by hitting the 🏓 ball towards the wall.".format(rank,counter), flush=True)
            else:
                if rank == 0:
                    print("Player {:d} started round {:d} by sending the 🏓 ball to Player {:d}.".format(rank,counter,sn), flush=True)
                else:
                    print("Player {:d} sent the 🏓 ball to Player {:d}.".format(rank,sn), flush=True)

    # Check if the player is bored
    bored = (counter >= max_count)

# Announce that we are done for the day.
if last == True:
    if size == 1:
        print("🎉 Player {:d} won the game of 🏓 ping pong, since they were playing alone! 🎉".format(rank), flush=True)
    else:
        print("🎉 Player {:d} won the game of 🏓 ping pong, since everyone else quit! 🎉".format(rank), flush=True)
else:
    print("🛑 Player {:d} is bored of 🏓 ping pong and is quitting! 🛑".format(rank), flush=True)
