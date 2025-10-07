from django.test import TestCase

# Create your tests here.



# async function addToCart(productId) {
#     try {
#         const response = await fetch(`/cart/add/${productId}/`, {
#             method: 'POST',
#             headers: {
#                 'X-CSRFToken': getCSRFToken(),
#                 'Content-Type': 'application/json',
#             },
#         });
#
#         const data = await response.json();
#
#         if (data.success) {
#
#             showNotification(data.message);
#         }
#     } catch (error) {
#         console.error('Error:', error);
#     }
# }