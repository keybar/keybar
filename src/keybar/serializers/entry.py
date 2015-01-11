from rest_framework import serializers


class VaultItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('created', 'id', 'name',  'owner', 'value', 'vault', )
        model = VaultItem
        read_only_fields = ('created', 'owner', )

    def __init__(self, *args, **kwargs):
        super(VaultItemSerializer, self).__init__(*args, **kwargs)
        vaultfield = self.fields['vault']
        uid = self.context.get('request').user.pk
        vaultfield.queryset = vaultfield.queryset.get_for_uid(uid)
