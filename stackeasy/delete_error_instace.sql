
use nova;

delete from instance_info_caches where instance_uuid in (select uuid from instances where vm_state='error');

delete from instance_metadata where instance_uuid in (select uuid from instances where vm_state='error');

delete from instance_system_metadata where instance_uuid in (select uuid from instances where vm_state='error');

delete from security_group_instance_association where instance_uuid in (select uuid from instances where vm_state='error');

delete from virtual_interfaces where instance_uuid in (select uuid from instances where vm_state='error');

update fixed_ips set instance_uuid=null where instance_uuid in (select uuid from instances where vm_state='error');

delete from instances where vm_state='error';