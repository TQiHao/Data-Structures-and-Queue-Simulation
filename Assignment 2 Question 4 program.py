import random

class Email:
    def __init__(self, id):
        self.id = id
        self.requeues = 0  # Track how many times it was requeued

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, email):
        self.queue.append(email)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

# Get user input for total minutes
SIMULATION_MINUTES = int(input("Please enter the total minutes to run: "))

# Constants
ARRIVAL_RATE = 30  # Emails per minute (average)
SEND_LIMIT = 30  # Max emails processed per minute
FAIL_RATE = 0.25  # 25% chance of failure

# Tracking statistics
total_messages = 0
total_sent = 0
total_requeues = 0
queue_size_per_minute = []
sent_attempts = {}

# Initialize queue
email_queue = Queue()
email_id = 1

# Simulation loop
for minute in range(1, SIMULATION_MINUTES + 1):
    # Randomized email arrivals (range: ~20 to 40 per minute)
    arrivals = random.randint(20, 40)
    total_messages += arrivals

    for _ in range(arrivals):
        email_queue.enqueue(Email(email_id))
        email_id += 1

    # Process emails (up to 30 per minute)
    emails_processed = 0
    for _ in range(SEND_LIMIT):
        if email_queue.is_empty():
            break

        email = email_queue.dequeue()
        emails_processed += 1

        if random.random() < FAIL_RATE:
            # Failed to send then requeue it
            email.requeues += 1
            email_queue.enqueue(email)
            total_requeues += 1
        else:
            # Successfully sent then track attempt
            attempt_num = email.requeues + 1
            sent_attempts[attempt_num] = sent_attempts.get(attempt_num, 0) + 1
            total_sent += 1

    queue_size_per_minute.append(email_queue.size())

# Final Statistics
average_arrival_rate = total_messages / SIMULATION_MINUTES
average_sent_per_minute = total_sent / SIMULATION_MINUTES
average_queue_size = sum(queue_size_per_minute) / SIMULATION_MINUTES
average_requeues = total_requeues / total_sent if total_sent > 0 else 0

# Display results
print("\nTotal number of messages processed      : {:.0f}".format(total_messages))
print("Average arrival rate                    : {:.2f}".format(average_arrival_rate))
print("Average number of messages sent per minute : {:.2f}".format(average_sent_per_minute))
print("Average number of messages in the queue per minute : {:.2f}".format(average_queue_size))

print("\nNumber of messages sent on 1st attempt    : {}".format(sent_attempts.get(1, 0)))
print("Number of messages sent on 2nd attempt    : {}".format(sent_attempts.get(2, 0)))
print("Number of messages sent on 3rd attempt    : {}".format(sent_attempts.get(3, 0)))
print("Number of messages sent on 4th attempt    : {}".format(sent_attempts.get(4, 0)))
print("Number of messages sent on 5th attempt    : {}".format(sent_attempts.get(5, 0)))

print("\nAverage number of times messages had to be requeued : {:.2f}".format(average_requeues))

print()
input("Press Enter to terminate")
