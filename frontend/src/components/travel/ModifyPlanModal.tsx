import React, { useState } from 'react';
import { View, Modal, Pressable } from 'react-native';
import { Card, CardHeader, CardTitle, CardContent, Button, buttonTextVariants, TextArea, Text } from '@/components/ui';
import { X } from '@/lib/icons';

interface ModifyPlanModalProps {
  visible: boolean;
  onClose: () => void;
  onSubmit: (feedback: string) => void;
  isLoading?: boolean;
}

export function ModifyPlanModal({
  visible,
  onClose,
  onSubmit,
  isLoading,
}: ModifyPlanModalProps) {
  const [feedback, setFeedback] = useState('');

  const handleSubmit = () => {
    if (feedback.trim()) {
      onSubmit(feedback.trim());
      setFeedback('');
    }
  };

  const handleClose = () => {
    setFeedback('');
    onClose();
  };

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={handleClose}
    >
      <Pressable
        className="flex-1 bg-black/50 justify-center items-center p-4"
        onPress={handleClose}
      >
        <Pressable onPress={(e) => e.stopPropagation()}>
          <Card className="w-full max-w-md">
            <CardHeader className="flex flex-row justify-between items-center">
              <CardTitle>계획 수정 요청</CardTitle>
              <Pressable onPress={handleClose} disabled={isLoading}>
                <X size={24} className="text-muted-foreground" />
              </Pressable>
            </CardHeader>
            <CardContent className="gap-4">
              <Text className="text-sm text-muted-foreground">
                수정하고 싶은 내용을 자세히 알려주세요. AI가 피드백을 반영하여 계획을 개선합니다.
              </Text>

              <TextArea
                placeholder="예: 첫째 날에 인사동을 추가해주세요. 더 저렴한 식당으로 변경해주세요."
                value={feedback}
                onChangeText={setFeedback}
                editable={!isLoading}
                className="min-h-[120px]"
              />

              <View className="flex flex-row gap-2">
                <Button
                  variant="outline"
                  onPress={handleClose}
                  disabled={isLoading}
                  className="flex-1"
                >
                  <Text className={buttonTextVariants({ variant: 'outline' })}>
                    취소
                  </Text>
                </Button>
                <Button
                  onPress={handleSubmit}
                  disabled={isLoading || !feedback.trim()}
                  className="flex-1"
                >
                  <Text className={buttonTextVariants()}>
                    {isLoading ? '수정 중...' : '수정 요청'}
                  </Text>
                </Button>
              </View>
            </CardContent>
          </Card>
        </Pressable>
      </Pressable>
    </Modal>
  );
}
