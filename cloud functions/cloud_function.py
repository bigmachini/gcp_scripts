import subprocess


def format_response(status, msg=None):
    res = {'status': status}
    if msg:
        res['message'] = msg
    return res


def validate_dict(required_fieds=[], data_dic={}):
    msg = []
    if required_fieds and data_dic:
        for _ in required_fieds:
            if _ not in data_dic:
                msg.append(f'{_}_required'.upper())
        if msg:
            return format_response(0, msg)
        else:
            return format_response(1)
    else:
        return format_response(0, 'Invalid Parameters')


def execute_script(vals):
    _fields = ['function_name', 'entry_point', 'runtime', 'region', 'stage_bucket', 'trigger_type']
    _validate_res = validate_dict(_fields, vals)

    if _validate_res and _validate_res['status']:
        function_name = vals['function_name']
        entry_point = vals['entry_point']
        runtime = vals['runtime']
        region = vals['region']
        stage_bucket = vals['stage_bucket']
        trigger_type = vals['trigger_type']
        bucket = vals.get('bucket', None)
        set_env = vals.get('set_env', None)
        memory = vals.get('memory', '128MB')
        service_account = vals.get('service_account', None)
        allow_unauthenticated = vals.get('allow_unauthenticated', False)

        cmd = f"gcloud functions deploy  {function_name} --entry-point={entry_point} --runtime={runtime} --region={region} --stage-bucket={stage_bucket} --memory={memory}"

        if service_account:
            cmd = f'{cmd} --service-account={service_account}'

        if allow_unauthenticated:
            cmd = f'{cmd} --allow-unauthenticated'

        if set_env:
            cmd = f'{cmd} --set-env-vars={set_env}'

        if trigger_type == 'http':
            cmd = f'{cmd} --trigger-http'
        elif trigger_type == 'bucket':
            cmd = f'{cmd} --trigger-bucket={bucket}'
        elif trigger_type == 'pub/sub':
            pass

        print(f"cmd: {cmd}")
        subprocess.call(cmd, shell=True)
    else:
        return _validate_res


if __name__ == '__main__':
    vals = {
        'function_name': 'function_name',
        'entry_point': 'function_name',
        'runtime': 'runtime',
        'region': 'region',
        'stage_bucket': 'stage_bucket',
        'trigger_type': 'trigger_type',
        'allow_unauthenticated': True,
    }
    execute_script(vals)

