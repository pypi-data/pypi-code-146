dict(
    flow=[
        dict(
            type="CropStage",
            params=dict(
                # 裁剪区域
                crop_rect=[190, 5, 480, 320]
            )
        ),
        dict(
            type="DetectionStage",
            params=dict(
                # 是否绘制关节点
                draw=True
            )
        ),
        dict(
            type="RuleStage",
        )
    ]
)
