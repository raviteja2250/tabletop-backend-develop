"""
    Declare the status for Order
"""

# The order is checked out and waiting to be paid
CHECKED_OUT = 'checked_out'

# The order is failed to be placed.
FAILED = 'failed'

# The order is send to kitchen
RECEIVED = 'received'

# Pending for discuss between kitchen and front_desk staff before reject
PENDING_REJECTION = 'pending_rejection'

# Kitchen rejected the order for some reason
REJECTED = 'rejected'

# Kitchen accepted to process the order
ACCEPTED = 'accepted'

# Kitchen started to prepare the order
COOKING = 'cooking'

# All items of order are cooked and process the packing
COOKED = 'cooked'

# All items of order are packed and we can send it.
READY_TO_SEND = 'ready_to_send'

# In deliverying
ON_THE_WAY = 'on_the_way'

# Complete
COMPLETED = 'completed'
