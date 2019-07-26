#-----------------------------------------------------------------------------
#Min     Hour    Day     Month   Weekday    Command
#-----------------------------------------------------------------------------
*/15    4-18      *        *       1-5      /usr/bin/python3 -m esmt.env_set.common.rundeck_ping_status
*/15    4-18      *        *       1-5      /usr/bin/python3 -m esmt.env_set.common.rundeck_interface_status
*/15    4-18      *        *       1-5      /usr/bin/python3 -m esmt.env.common.rundeck_get_service_status soc-r3
*/15    4-18      *        *       1-5      /usr/bin/python3 -m esmt.env.common.rundeck_get_service_status soc-r2
*/300   4-18      *        *       1-5      /usr/bin/python3 -m esmt.env.common.rundeck_get_store_facts r3
*/300   4-18      *        *       1-5      /usr/bin/python3 -m esmt.env.common.rundeck_get_store_facts r2
*/300   4-18      *        *       1-5      /usr/bin/python3 -m esmt.env.common.rundeck_get_mount_details r3
*/300   4-18      *        *       1-5      /usr/bin/python3 -m esmt.env.common.rundeck_get_mount_details r2
