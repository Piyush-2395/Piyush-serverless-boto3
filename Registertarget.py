def register_targets(target_group_arn, instance_ids):
    response = elbv2.register_targets(
        TargetGroupArn = target_group_arn, 
        Targets = [{'Id': insatnce_id}for instance_id in instance_ids]
    )
    print("Target registered:", response)