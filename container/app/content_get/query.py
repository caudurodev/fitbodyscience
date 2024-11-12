"""useful queries for content_get"""

# query GetContentTreeQuery($contentId: uuid!) {
#   content(where: {id: {_eq: $contentId}}) {
#     id
#     content_type
#   }
#   content_relationship(where: {parent_content_id: {_eq: $contentId}}) {
#     child_content_id
#     child_content {
#       id
#       media_type
#       content_type
#     }
#   }
# }
# {
#   "contentId": "ab2bdcbe-b6fc-4ec9-9009-5b5f135ddd1a"
# }
